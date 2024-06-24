from apps import db
import datetime 
from sqlalchemy.orm import relationship
class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    description = db.Column(db.Text)
    language = db.Column(db.String(50))
    actions_state = db.Column(db.JSON)
    personality_traits = db.Column(db.JSON)
    state_of_mind = db.Column(db.JSON)
    character_scenes = db.Column(db.JSON)
    long_term_memory = db.Column(db.Boolean)
    node_based_story = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    configure_avatar = db.Column(db.Text)
    knowledge_bank = db.Column(db.Text)
    memory = db.Column(db.JSON)
    settings = db.Column(db.JSON)
    safety = db.Column(db.JSON)
    safety_status = db.Column(db.Boolean)
    hobbies = db.Column(db.JSON)
    pronouns = db.Column(db.String(255))
    role = db.Column(db.String(255))
    age = db.Column(db.Integer)
    alternative_name = db.Column(db.JSON)
    motivation = db.Column(db.Text)
    flaws = db.Column(db.Text)
    wikipedia_link = db.Column(db.Text)
    wikipedia_link_status = db.Column(db.Boolean)
    yaml_editor_status = db.Column(db.Boolean)
    dialogue_structure = db.Column(db.Text)
    personal_knowledge = db.Column(db.Text)
    created_at = db.Column(db.Float, nullable=False)
    avatar_url =  db.Column(db.Text)
    yaml_file_path =  db.Column(db.Text)
    stage_of_life =  db.Column(db.Text)
    alternative_names =  db.Column(db.Text)
    hobbies_and_interests =  db.Column(db.Text)
    avatar_key =  db.Column(db.Text)
    dialogue_style =  db.Column(db.Text)
    knowledge_filters =  db.Column(db.Text)
    common_knowledge =  db.Column(db.Text)
    workspace = relationship('Workspace', back_populates='character')

    # knowledge = relationship('Knowledge', back_populates='character')

    def __init__(self, workspace_id, name, avatar, description, language, actions_state, personality_traits, state_of_mind, character_scenes, long_term_memory, node_based_story, deleted, active, configure_avatar, knowledge_bank, memory, settings, safety, safety_status, hobbies, pronouns, role, age, alternative_name, motivation, flaws, wikipedia_link, wikipedia_link_status, yaml_editor_status, dialogue_structure, personal_knowledge, created_at):
        
        self.workspace_id = workspace_id
        self.name = name
        self.avatar = avatar
        self.description = description
        self.language = language
        self.actions_state = actions_state
        self.personality_traits = personality_traits
        self.state_of_mind = state_of_mind
        self.character_scenes = character_scenes
        self.long_term_memory = long_term_memory
        self.node_based_story = node_based_story
        self.deleted = deleted
        self.active = active
        self.configure_avatar = configure_avatar
        self.knowledge_bank = knowledge_bank
        self.memory = memory
        self.settings = settings
        self.safety = safety
        self.safety_status = safety_status
        self.hobbies = hobbies
        self.pronouns = pronouns
        self.role = role
        self.age = age
        self.alternative_name = alternative_name
        self.motivation = motivation
        self.flaws = flaws
        self.wikipedia_link = wikipedia_link
        self.wikipedia_link_status = wikipedia_link_status
        self.yaml_editor_status = yaml_editor_status
        self.dialogue_structure = dialogue_structure
        self.personal_knowledge = personal_knowledge
        self.created_at = created_at
