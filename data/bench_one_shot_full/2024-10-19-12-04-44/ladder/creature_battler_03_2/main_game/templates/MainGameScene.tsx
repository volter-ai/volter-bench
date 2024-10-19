import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { Shield, Zap, Activity } from 'lucide-react';

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
    attack: number;
    defense: number;
    speed: number;
  };
  meta: {
    creature_type: string;
  };
  collections: {
    skills: Skill[];
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="flex flex-col h-screen w-full bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={props.data.entities.player.uid}
          playerName={props.data.entities.player.display_name}
          imageUrl="/path/to/player/image.jpg"
        />
        <PlayerCard
          uid={props.data.entities.opponent.uid}
          playerName={props.data.entities.opponent.display_name}
          imageUrl="/path/to/opponent/image.jpg"
        />
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/path/to/${playerCreature.meta.creature_type}_creature.jpg`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <Shield className="text-blue-500" />
            <span>{playerCreature.stats.defense}</span>
            <Zap className="text-yellow-500" />
            <span>{playerCreature.stats.speed}</span>
            <Activity className="text-red-500" />
            <span>{playerCreature.stats.attack}</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/path/to/${opponentCreature.meta.creature_type}_creature.jpg`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <Shield className="text-blue-500" />
            <span>{opponentCreature.stats.defense}</span>
            <Zap className="text-yellow-500" />
            <span>{opponentCreature.stats.speed}</span>
            <Activity className="text-red-500" />
            <span>{opponentCreature.stats.attack}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
            />
          ))}
        </div>
        <div className="mt-4 flex justify-center space-x-4">
          {availableButtonSlugs.includes('quit-game') && (
            <Button onClick={() => emitButtonClick('quit-game')}>Quit Game</Button>
          )}
          {availableButtonSlugs.includes('return-to-main-menu') && (
            <Button onClick={() => emitButtonClick('return-to-main-menu')}>Return to Main Menu</Button>
          )}
        </div>
      </div>
    </div>
  );
}
