from config import db
from flask import Blueprint, jsonify, request
from controllers import pokemonController


router = Blueprint("pokemon", __name__)


@router.route("/api/pokemon/<pokemon_identifier>", methods=["GET"])
def pokemon(pokemon_identifier):
    return pokemonController.getPokemonByName(pokemon_identifier)


@router.route("/api/form_team", methods=["POST"])
def form_team():
    data = request.json
    return pokemonController.formTeam(data)


# Nova rota para listar todos os times registrados
@router.route("/api/teams", methods=["GET"])
def list_teams():
    return pokemonController.listTeams()


# Nova rota para buscar um time registrado por usuário
@router.route("/api/teams/<string:owner>", methods=["GET"])
def get_team_by_owner(owner):
    return pokemonController.listTeamsByOwner(owner)


# Nova rota para deletar um time registrado por usuário
# Para implementar essa rota sera nesse
@router.route(
    "/api/teams/delete/<string:owner_name>/<string:team_id>", methods=["DELETE"]
)
def delete_team(owner_name, team_id):
    return pokemonController.deleteTeam(owner_name, team_id)
