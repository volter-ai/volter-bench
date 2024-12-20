import { useCurrentButtons } from "@/lib/useChoices.ts";
import { ArrowLeft } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    skill_type: string;
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <h1 className="text-xl font-bold">Battle Arena</h1>
        {availableButtonSlugs.includes('return-to-main-menu') && (
          <Button
            onClick={() => emitButtonClick('return-to-main-menu')}
            className="flex items-center"
          >
            <ArrowLeft className="mr-2" size={16} />
            Main Menu
          </Button>
        )}
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={props.data.entities.player.uid}
            playerName={props.data.entities.player.display_name}
            imageUrl="/path/to/player-image.jpg"
            className="mb-4"
          />
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl="/path/to/creature-image.jpg"
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={props.data.entities.opponent.uid}
            playerName={props.data.entities.opponent.display_name}
            imageUrl="/path/to/opponent-image.jpg"
            className="mb-4"
          />
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl="/path/to/creature-image.jpg"
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <h2 className="text-lg font-semibold mb-2">Skills</h2>
        <div className="grid grid-cols-2 gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
