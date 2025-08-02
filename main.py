p><strong>Результат установки:</strong> {'✅ Успешно' if result else '❌ Ошибка'}</p>
            
            <h2>Текущее состояние webhook:</h2>
            <pre>{current_webhook}</pre>
            
            <h2>Тестирование бота:</h2>
            <p>Теперь попробуйте отправить <code>/start</code> боту @GrammerBuddyBot в Telegram</p>
            
            <p><a href="/">← Вернуться на главную</a></p>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''
        <h1>❌ Ошибка: {str(e)}</h1>
        <p>Возможные причины:</p>
        <ul>
            <li>Неверный токен бота</li>
            <li>Проблемы с сетью</li>
            <li>URL должен быть HTTPS</li>
        </ul>
        <p><a href="/">← Вернуться на главную</a></p>
        '''


    """Basic index page."""
    webhook_setup_url = request.url_root.rstrip('/') + '/setup_webhook'
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>English Learning Bot</title>
        <meta charset="UTF-8">
    </head>
    <body>
