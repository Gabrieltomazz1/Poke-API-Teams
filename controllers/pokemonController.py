from config import db
from flask import jsonify
from models.pokemonModel import Pokemon, Owner, Team
import requests


def get_pokemon(pokemon_identifier):
    # Tentar obter o Pokémon do banco de dados
    pokemon = Pokemon.query.filter_by(name=pokemon_identifier).first()

    if pokemon:
        # Se o Pokémon existe no banco de dados, retornar suas informações
        return {
            "api_id": pokemon.api_id,  # Inclua o ID da API na resposta
            "name": pokemon.name,
            "height": pokemon.height,
            "weight": pokemon.weight,
        }
    else:
        # Se o Pokémon não está no banco de dados, fazer a chamada à API
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_identifier}/"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                # Adicionar o Pokémon ao banco de dados antes de retornar suas informações
                new_pokemon = Pokemon(
                    api_id=response.json()[
                        "id"
                    ],  # Salvar o ID da API no banco de dados
                    name=pokemon_identifier,
                    height=response.json()["height"],
                    weight=response.json()["weight"],
                )
                db.session.add(new_pokemon)
                db.session.commit()

                return {
                    "api_id": new_pokemon.api_id,  # Inclua o ID da API na resposta
                    "name": new_pokemon.name,
                    "height": new_pokemon.height,
                    "weight": new_pokemon.weight,
                }
            else:
                print(
                    f"Erro na solicitação para Pokémon {pokemon_identifier}: {response.status_code}"
                )
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro na solicitação para Pokémon {pokemon_identifier}: {e}")
            return None


def getPokemonByName(pokemon_identifier):
    pokemon_data = get_pokemon(pokemon_identifier)
    if pokemon_data:
        pokemon_info = {
            "api_id": pokemon_data["api_id"],
            "name": pokemon_data["name"],
            "height": pokemon_data["height"],
            "weight": pokemon_data["weight"],
        }

        lista = [pokemon_info]
        return jsonify(lista)
    else:
        return (
            jsonify({"Message": f"Pokemon '{pokemon_identifier}' não encontrado"}),
            404,
        )


def formTeam(data):
    if "owner" in data and "team" in data:
        owner_name = data["owner"]
        team_pokemon_names = data["team"]

        # Verificar se o usuário existe no banco de dados
        owner = Owner.query.filter_by(name=owner_name).first()
        if not owner:
            owner = Owner(name=owner_name)
            db.session.add(owner)

        # Criar e adicionar os Pokémon à equipe
        team = Team(owner=owner)
        for pokemon_name in team_pokemon_names:
            pokemon_info = get_pokemon(pokemon_name)

            if pokemon_info:
                # Adicionar o Pokémon à equipe
                team_pokemon = Pokemon(
                    name=pokemon_info["name"],
                    api_id=pokemon_info["api_id"],
                    height=pokemon_info["height"],
                    weight=pokemon_info["weight"],
                )
                team.pokemons.append(team_pokemon)

        # Adicionar a equipe ao banco de dados
        db.session.add(team)
        db.session.commit()

        # Construir o output desejado
        output = {}
        for idx, team in enumerate(owner.teams, start=1):
            team_data = {
                "owner": owner.name,
                "pokemons": [
                    {
                        "api_id": pokemon.api_id,
                        "name": pokemon.name,
                        "weight": pokemon.weight,
                        "height": pokemon.height,
                    }
                    for pokemon in team.pokemons
                ],
            }
            output[idx] = team_data

        return jsonify(output)
    else:
        return jsonify({"Message": "Dados inválidos"}), 400


def listTeams():
    teams_data = {}
    for idx, team in enumerate(Team.query.all(), start=1):
        team_data = {
            "owner": team.owner.name,
            "pokemons": [
                {
                    "api_id": pokemon.api_id,
                    "name": pokemon.name,
                    "weight": pokemon.weight,
                    "height": pokemon.height,
                }
                for pokemon in team.pokemons
            ],
        }
        teams_data[idx] = team_data
    return jsonify(teams_data)


def listTeamsByOwner(owner):
    owner = Owner.query.filter_by(name=owner).first()

    if owner:
        teams_data = {}
        for idx, team in enumerate(owner.teams, start=1):
            team_data = {
                "owner": owner.name,
                "pokemons": [
                    {
                        "id": pokemon.id,
                        "name": pokemon.name,
                        "weight": pokemon.weight,
                        "height": pokemon.height,
                    }
                    for pokemon in team.pokemons
                ],
            }
            teams_data[str(idx)] = team_data  # Usar a string do índice como chave

        return jsonify(teams_data)
    else:
        return (
            jsonify({"Message": f"Nenhum time encontrado para o usuário '{owner}'"}),
            404,
        )


def deleteTeam(owner_name, team_id):
    owner = Owner.query.filter_by(name=owner_name).first()
    team = Team.query.filter_by(id=team_id).first()
    if owner and team:
        # Remover a equipe do relacionamento com o owner)
        owner.teams.remove(team)

        db.session.delete(team)
        db.session.commit()
        return jsonify({"Message": "Team deleted successfully"})
    return jsonify({"Message": "Team or owner not found"}), 404
