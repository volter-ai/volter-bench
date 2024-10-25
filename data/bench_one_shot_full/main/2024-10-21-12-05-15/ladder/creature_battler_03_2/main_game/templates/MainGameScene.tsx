import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { Sword, Shield, Zap } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

const ButtonArea = ({ availableButtonSlugs, emitButtonClick, playerSkills }: {
  availableButtonSlugs: string[];
  emitButtonClick: (slug: string) => void;
  playerSkills: Skill[];
}) => {
  return (
    <div className="flex flex-wrap justify-center gap-2 p-4">
      {availableButtonSlugs.includes('play-again') && (
        <Button onClick={() => emitButtonClick('play-again')}>Play Again</Button>
      )}
      {availableButtonSlugs.includes('quit') && (
        <Button onClick={() => emitButtonClick('quit')}>Quit</Button>
      )}
      {playerSkills.map((skill) => (
        <SkillButton
          key={skill.uid}
          uid={skill.uid}
          skillName={skill.display_name}
          description={skill.description}
          stats={`Damage: ${skill.stats.base_damage}`}
          onClick={() => emitButtonClick(skill.uid)}
        />
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
      <div className="bg-gray-800 text-white p-2 flex justify-between">
        <span>{player?.display_name}</span>
        <span>VS</span>
        <span>{opponent?.display_name}</span>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {player_creature && (
          <div className="flex flex-col items-center">
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              imageUrl={`/images/creatures/${player_creature.meta.prototype_id}.png`}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
            />
            <div className="mt-2 flex gap-2">
              <span title="Attack"><Sword size={16} /> {player_creature.stats.attack}</span>
              <span title="Defense"><Shield size={16} /> {player_creature.stats.defense}</span>
              <span title="Speed"><Zap size={16} /> {player_creature.stats.speed}</span>
            </div>
          </div>
        )}
        {opponent_creature && (
          <div className="flex flex-col items-center">
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              imageUrl={`/images/creatures/${opponent_creature.meta.prototype_id}.png`}
              hp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
            />
            <div className="mt-2 flex gap-2">
              <span title="Attack"><Sword size={16} /> {opponent_creature.stats.attack}</span>
              <span title="Defense"><Shield size={16} /> {opponent_creature.stats.defense}</span>
              <span title="Speed"><Zap size={16} /> {opponent_creature.stats.speed}</span>
            </div>
          </div>
        )}
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <ButtonArea
          availableButtonSlugs={availableButtonSlugs}
          emitButtonClick={emitButtonClick}
          playerSkills={player_creature?.collections.skills ?? []}
        />
      </div>
    </div>
  );
}
