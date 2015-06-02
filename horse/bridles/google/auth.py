import pickle

import sqlobject
from oauth2client.client import OAuth2WebServerFlow

from horse import config
from horse import models
from horse.bridles.base import BridleModel
from horse.bridles.base import WebhookBridle
from horse.bridles.base import CommandBridle

AUTH_CALLBACK_PATH = 'auth/google'


class GoogleAuthFlow(BridleModel):
    user = sqlobject.ForeignKey('User')
    flow = sqlobject.StringCol()

    def get_flow(self):
        return pickle.loads(self.flow)


class GoogleAuthCredentials(BridleModel):
    user = sqlobject.ForeignKey('User')
    credentials = sqlobject.StringCol()

    def get_credentials(self):
        return pickle.loads(self.credentials)


class GoogleAuthMixin(object):

    def _get_auth_flow(self, user, new_flow=False):
        flow_record = None
        if not new_flow:
            flow_record = GoogleAuthFlow.selectBy(user=user).getOne(None)

        if flow_record is None:
            flow = OAuth2WebServerFlow(
                client_id=config.GAPI_CLIENT_ID,
                client_secret=config.GAPI_CLIENT_SECRET,
                scope=" ".join(config.GAPI_SCOPES),
                redirect_uri="http://{0}/{1}".format(
                    config.HOSTNAME,
                    AUTH_CALLBACK_PATH
                ),
                state=user.string_id
            )
            flow_record = GoogleAuthFlow(
                user=user,
                flow=pickle.dumps(flow)
            )
        else:
            flow = flow_record.get_flow()

        return flow

    def authorize(self, user):
        flow = self._get_auth_flow(user, new_flow=True)
        self.message(
            user,
            "Please <{0}|click here> to authorize your Google account.".format(
                flow.step1_get_authorize_url()
            )
        )

    def get_credentials(self, user):
        credentials = GoogleAuthCredentials.selectBy(user=user).getOne(None)
        if credentials is None:
            self.authorize(user)
            return None
        else:
            return credentials.get_credentials()


class GoogleAuthCallback(WebhookBridle):

    class Meta(WebhookBridle.Meta):
        path = AUTH_CALLBACK_PATH

    def execute(self, path, params):
        user = models.User.selectBy(string_id=params['state']).getOne(None)
        if user is None:
            return "Unknown user."

        flow_record = GoogleAuthFlow.selectBy(user=user).getOne(None)
        if user is None:
            return "No auth flow found."

        flow = pickle.loads(flow_record.flow)
        credentials = flow.step2_exchange(params['code'])
        print credentials
        GoogleAuthCredentials(
            user=user,
            credentials=pickle.dumps(credentials)
        )
        self.message(user, "Your account has been authorized")


class GoogleAuthInit(CommandBridle, GoogleAuthMixin):

    class Meta(CommandBridle.Meta):
        command = 'gauth'

    def execute(self, user, channel, operands):
        if self.get_credentials(user):
            return "Already authorized."
