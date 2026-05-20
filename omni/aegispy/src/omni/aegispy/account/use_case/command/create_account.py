from omni.aegispy.src.omni.aegispy.account.domain import Account, AccountInputDto, AccountRepository
from omni.aegispy.src.omni.aegispy.shared import Command, CommandHandler


class CreateAccount(Command, AccountInputDto):
    pass


class CreateAccountHandler(CommandHandler):
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    async def handle(self, command: CreateAccount) -> Account:
        account = Account.create(command)

        await self.repository.save(account)

        return account
