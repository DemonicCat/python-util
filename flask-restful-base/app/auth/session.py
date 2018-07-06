from flask.sessions import SessionInterface, SessionMixin
from pyutil.data.session.session import Session
import datetime

class WebSessionInterface(SessionInterface):
    DEFAULT_SESSION_AGE = 24 * 3600 * 7

    def _get_session_key(self, app, request):
        url_session_key = request.args.get('token', None)
        url_session_key = url_session_key.strip() if url_session_key else None
        token_session_key = request.headers.get('token', None)
        session_key = url_session_key or token_session_key or \
                      request.cookies.get(app.session_cookie_name, None)
        if session_key is None:
            get_key = app.config.get('SESSION_GET_NAME', 'session_key')
            session_key = request.args.get(get_key, None)
        return session_key

    def open_session(self, app, request):
        session_key = self._get_session_key(app, request)
        session = Session(session_key)
        return session

    def save_session(self, app, session, response):
        if len(session.keys()) == 0:
            # we don't want to save empty session
            return response

        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)

        session.save()
        expiry_age = session.get_expiry_age()
        # update expiry if needed
        if expiry_age < self.DEFAULT_SESSION_AGE * 0.6:
            expiry_age = self.DEFAULT_SESSION_AGE
            session.set_expiry(self.DEFAULT_SESSION_AGE)

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.DEFAULT_SESSION_AGE)
        #response.set_cookie(app.session_cookie_name, session.session_key,
         #                   expires=expires, httponly=httponly,
          #                  domain=domain, path=path, secure=secure)
