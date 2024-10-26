import { useCurrentButtons } from "@/lib/useChoices.ts";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield, Zap } from 'lucide-react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  description: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

const ButtonPanel = ({ availableButtonSlugs, emitButtonClick }) => {
  const buttonConfig = {
    'play-again': { label: 'Play Again', icon: <Zap className="mr-2 h-4 w-4" /> },
    'quit': { label: 'Quit', icon: <Shield className="mr-2 h-4 w-4" /> },
  };

  return (
    <div className="flex space-x-2">
      {availableButtonSlugs.map((slug) => (
        <button
          key={slug}
          className="flex items-center px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          onClick={() => emitButtonClick(slug)}
        >
          {buttonConfig[slug]?.icon}
          {buttonConfig[slug]?.label || slug}
        </button>
      ))}
    </div>
  );
};

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={player.uid}
            playerName={player.display_name}
            imageUrl="/path/to/player/image.png"
          />
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl="/path/to/creature/image.png"
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={opponent.uid}
            playerName={opponent.display_name}
            imageUrl="/path/to/opponent/image.png"
          />
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl="/path/to/creature/image.png"
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-200">
        <div className="mb-4">
          <h2 className="text-lg font-semibold mb-2">Skills</h2>
          <div className="flex space-x-2">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
              />
            ))}
          </div>
        </div>
        <ButtonPanel
          availableButtonSlugs={availableButtonSlugs}
          emitButtonClick={emitButtonClick}
        />
      </div>
    </div>
  );
}
