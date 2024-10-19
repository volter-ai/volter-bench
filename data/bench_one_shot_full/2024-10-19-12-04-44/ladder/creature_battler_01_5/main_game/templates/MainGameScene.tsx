import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Player {
  uid: string;
  display_name: string;
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

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <Shield className="mr-2" />
          <span>Player: {props.data.entities.player?.display_name}</span>
        </div>
        <div className="flex items-center">
          <span>Opponent: {props.data.entities.opponent?.display_name}</span>
          <Swords className="ml-2" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <span className="mb-2">Player</span>
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl="/placeholder-creature.jpg"
              hp={playerCreature.stats.hp}
            />
          )}
        </div>
        <div className="flex flex-col items-center">
          <span className="mb-2">Opponent</span>
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl="/placeholder-creature.jpg"
              hp={opponentCreature.stats.hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/3 overflow-y-auto">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature?.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              onClick={() => emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
