from cryptoinvestor import application, views, main

views.BaseView.app = main.App()


if __name__ == '__main__':
    application.run()
