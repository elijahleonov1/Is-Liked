import vk
from time import sleep

session = vk.AuthSession(access_token='ACCESS_TOKEN')
api = vk.API(session)


class SearchLikes:
    """

    Получение постов группы и проверка на лайки.

    domain - короткий адрес группы или id.
    user_id - id пользователя которого нужно проверить.
    count - количество получаемых постов за один разю
    offset - смещение постов.
    post_num - счетчик проверенныъ постов.

    get_well - возращает посты из группы.
    is_liked - проверяет на лайки.
    run - используеться для проверки более 100 постов.

    """

    def __init__(self, user_id='', domain='', count=1, offset=0):
        self.domain = domain
        self.count = count
        self.offset = offset
        self.user_id = user_id
        self.post_num = 0

    def get_well(self):

        attachments = []
        posts = api.wall.get(domain=self.domain, count=self.count, offset=self.offset)

        for post in posts:
            if int is type(post):
                continue
            if post.setdefault('attachments'):
                for pst in post['attachments']:
                    if pst.setdefault('photo'):
                        photo = pst['photo']['src_big']
                        attachments.append({'id': post['id'], 'to_id': post['to_id'],
                                            'photo': photo, 'domain': self.domain})
        return attachments

    def is_liked(self, attachments, count_post=1):

        links = []
        num = 0

        for att in attachments:

            sleep(2)
            likes = api.likes.isLiked(user_id=self.user_id, type='post',
                                      owner_id=att['to_id'], item_id=att['id'])
            self.post_num += 1
            print('{} __ Проверенно постов'.format(self.post_num))

            if 1 is likes:
                num += 1
                url = 'https://vk.com/{}?w=wall{}_{}'.format(att['domain'], att['to_id'], att['id'])
                links.append({'url': url, 'photo': att['photo']})
                print('Лайк зафиксирован __ {} __ {} __ {}'.format(num, url, att['photo']))

            if count_post is self.post_num:
                break

        return links

    def run(self, count_post):
        while True:

            sleep(2)
            attachments = self.get_well()
            self.is_liked(attachments, count_post)

            if count_post is self.post_num:
                print('Конц')
                break

            print('{} __ Смещение'.format(self.offset))
            self.offset += 100


if __name__ == '__main__':
    SearchLikes(user_id='USER_ID', domain='GROUP_ID', count=100, offset=0).run(1010)
