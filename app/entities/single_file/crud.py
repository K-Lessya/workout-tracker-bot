from mongoengine import *
from .models import Trainer, Client, Training, ClientRequests


def create_trainer(trainer: Trainer):
    return trainer.save()


def get_client_by_username(tg_username: str):
    return Client.objects(tg_username=tg_username).first()

def get_client_by_id(tg_id: int):
    return Client.objects(tg_id=tg_id).first()

def update_client_trainer(client: Client, trainer: Trainer):
    client.trainer = trainer
    client.save()
    return True

def get_trainer(tg_id: int):
    return Trainer.objects(tg_id=tg_id).first()

def get_trainer_by_obj_id(obj_id: str):
    return Trainer.objects(id=obj_id).first()


def create_client(client: Client):
    client.save()
    client_requests = ClientRequests(client=client,
                                     trainers=[])
    client_requests.save()
    return True


def fill_client_name_surname(tg_username: str, tg_id: int, name: str, surname:str):
    client = Client.objects(tg_username=tg_username).first()
    client.tg_id = tg_id
    client.name = name
    client.surname = surname
    client.save()


def client_add_new_trainer_request(client: Client, trainer: Trainer):
    requests = ClientRequests.objects(client=client).first()
    requests.trainers.append(trainer)
    requests.save()


def client_delete_trainer_request(client: Client, trainer: Trainer):
    requests = ClientRequests.objects(client=client).first()
    requests.trainers.remove(trainer)
    return True


def client_get_num_trainier_requests(client: Client) -> int:
    request = ClientRequests.objects(client=client).first()
    return len(request.trainers)



def get_all_not_assigned_clients_with_name():
    return Client.objects(name__exists=True, trainer__exists=False, visibility=True)


def get_client_requests_by_id(tg_id):
    client = Client.objects(tg_id=tg_id).first()
    requests = ClientRequests.objects(client=client).first()
    return requests.trainers


def get_trainer_clients(first: int, range: int, trainer_id):
    clients = Client.objects(name__exists=True, trainer=trainer_id)[first:range]
    return clients


def create_training(tg_id: int, training: Training):
    client = Client.objects(tg_id=tg_id).first()
    client.trainings.append(training)
    client.save()
    return True



def delete_client_or_trainer(tg_id: int):
    client = Client.objects(tg_id=tg_id)
    if client:
        client.delete()
    else:
        trainer = Trainer.objects(tg_id=tg_id)
        if trainer:
            trainer.delete()
    return True
# @mongo_connection
# def check_user(telegram_id):
#     return mongo.db.users.find_one({'_id': telegram_id})
#
#
#
#
# @mongo_connection
# def create_first_wallet(telegram_id, name):
#     return mongo.db.wallets.insert_one(
#         {
#             'owner_id': telegram_id,
#             'balance': 0,
#             'name': name
#         }
#     )