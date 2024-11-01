import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={player.uid}
          playerName={player.display_name}
          imageUrl="/placeholder-player.jpg"
          className="w-auto h-12 flex items-center bg-blue-700"
        />
        <PlayerCard
          uid={opponent.uid}
          playerName={opponent.display_name}
          imageUrl="/placeholder-opponent.jpg"
          className="w-auto h-12 flex items-center bg-blue-700"
        />
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={player_creature.uid}
          name={player_creature.display_name}
          imageUrl="/placeholder-creature.jpg"
          hp={player_creature.stats.hp}
          className="transform scale-x-[-1]"
        />
        <CreatureCard
          uid={opponent_creature.uid}
          name={opponent_creature.display_name}
          imageUrl="/placeholder-creature.jpg"
          hp={opponent_creature.stats.hp}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="mb-4 h-24 bg-gray-200 p-2 rounded overflow-y-auto">
          {/* Game description text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {player_creature.collections.skills.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes('use-skill')}
            />
          ))}
          {availableButtonSlugs.includes('quit') && (
            <SkillButton
              uid="quit-button"
              skillName="Quit"
              description="Exit the current battle"
              stats=""
              onClick={() => emitButtonClick('quit')}
              className="bg-red-500 hover:bg-red-600"
            />
          )}
        </div>
      </div>
    </div>
  );
}
