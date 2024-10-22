import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Sword, Shield, Zap } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  meta: { skill_type: string };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: { hp: number; max_hp: number; attack: number; defense: number; speed: number };
  meta: { creature_type: string };
  uid: string;
  display_name: string;
  collections: { skills: Skill[] };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: { creatures: Creature[] };
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
        <span>{props.data.entities.player.display_name}</span>
        <span>{props.data.entities.opponent.display_name}</span>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/images/creatures/${playerCreature.meta.creature_type}.png`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <Sword size={20} /> <span>{playerCreature.stats.attack}</span>
            <Shield size={20} /> <span>{playerCreature.stats.defense}</span>
            <Zap size={20} /> <span>{playerCreature.stats.speed}</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/images/creatures/${opponentCreature.meta.creature_type}.png`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <Sword size={20} /> <span>{opponentCreature.stats.attack}</span>
            <Shield size={20} /> <span>{opponentCreature.stats.defense}</span>
            <Zap size={20} /> <span>{opponentCreature.stats.speed}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <Card className="p-4 bg-white">
        <div className="grid grid-cols-2 gap-2">
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
          {availableButtonSlugs.includes('play-again') && (
            <Button onClick={() => emitButtonClick('play-again')}>Play Again</Button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <Button onClick={() => emitButtonClick('quit')}>Quit</Button>
          )}
        </div>
      </Card>
    </div>
  );
}
