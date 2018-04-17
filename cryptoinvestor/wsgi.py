from cryptoinvestor import views, main

views.BaseView.app = main.App()

application = main.application

if __name__ == '__main__':
    application.run()
