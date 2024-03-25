from config import db

pokemon_team_association = db.Table(
    "pokemon_team_association",
    db.Column("pokemon_id", db.Integer, db.ForeignKey("pokemon.id")),
    db.Column("team_id", db.Integer, db.ForeignKey("team.id")),
)


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teams = db.relationship("Team", backref="owner", lazy=True)


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    teams = db.relationship(
        "Team", secondary=pokemon_team_association, back_populates="pokemons"
    )


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"), nullable=False)
    pokemons = db.relationship(
        "Pokemon", secondary=pokemon_team_association, back_populates="teams"
    )