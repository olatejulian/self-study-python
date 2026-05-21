from fastapi import FastAPI

from omni.aegispy.src.omni.aegispy.app.app_container import AppContainer
from omni.aegispy.src.omni.aegispy.app.domain import App
from omni.aegispy.src.omni.aegispy.app.presentation import (
    loginRouter,
    signupRouter,
    verifyEmailRouter,
)


def bootstrap(container=AppContainer()) -> FastAPI:
    application = App(container, [signupRouter, verifyEmailRouter, loginRouter])

    return application.get_api()
