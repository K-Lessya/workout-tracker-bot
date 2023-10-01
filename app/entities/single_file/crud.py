from mongoengine import *
from .models import Trainer, Client, Training, ClientRequests


def create_trainer(trainer: Trainer):
    return trainer.save()


def get_client_by_username(tg_username: str):
    return Client.objects(tg_username=tg_username).first()


def get_client(obj_id: str):
    return Client.objects(id=obj_id).first()

def get_all_clients():
    return Client.objects()

def get_all_trainers():
    return Trainer.objects()

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


def get_trainer_by_username(tg_username: str):
    return Trainer.objects(tg_username=tg_username).first()


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
    requests.save()
    return True


def client_get_num_trainier_requests(client: Client) -> int:
    request = ClientRequests.objects(client=client).first()

    return len(request.trainers)



def get_all_not_assigned_clients_with_name():
    return Client.objects(name__exists=True, trainer__exists=False, visibility=True).order_by('name', 'surname')


def get_client_requests_by_id(tg_id):
    client = Client.objects(tg_id=tg_id).first()
    requests = ClientRequests.objects(client=client).first()
    return requests.trainers


def get_trainer_clients_range(first: int, range: int, trainer_id):
    clients = Client.objects(name__exists=True, trainer=trainer_id)[first:range]
    return clients


def get_trainer_clients(trainer: Trainer):
    clients = Client.objects(name__exists=True, trainer=trainer).order_by('name', 'surname')
    return clients

def get_trainer_clients_witout_name(trainer: Trainer):
    clients = Client.objects(name__exists=False, trainer=trainer)
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

def get_all_client_trainigs(tg_id):
    client = Client.objects(tg_id=tg_id).first()
    trainings = client.trainings
    return trainings

def get_client_trainings(tg_id: int, start_pos, range):
    client = Client.objects(tg_id=tg_id).first()
    trainings = client.trainings
    if trainings:
        pipeline = [
            {'$match': {'tg_id': tg_id}},
            {'$project': {
                '_id': 0,
                'selected_trainings': {
                    '$map': {
                        'input': {'$slice': ['$trainings', start_pos, range]},
                        'as': 'item',
                        'in': {
                            'index': {'$indexOfArray': ['$trainings', '$$item']},
                            'value': '$$item'
                        }
                    }
                },
                'length': {'$size': '$trainings'}}
             }
        ]
        client_trainings = list(Client.objects.aggregate(*pipeline))
        print(client_trainings)
        return client_trainings
    else:
        return [[]]


def get_client_training(tg_id, training_id):
    client = Client.objects(tg_id=tg_id).first()
    return client.trainings[training_id]