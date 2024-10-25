import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap, Heart } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    creature_type: string;
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
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

  const { player_creature, opponent_creature } = props.data.entities;

  const renderCreatureStats = (creature: Creature) => (
    <div className="flex flex-col items-start p-2 bg-gray-100 rounded-lg">
      <h3 className="text-lg font-bold mb-2">{creature.display_name}</h3>
      <div className="w-full bg-gray-300 h-4 rounded-full overflow-hidden mb-2">
        <div
          className="bg-green-500 h-full"
          style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
        ></div>
      </div>
      <p className="text-sm">HP: {creature.stats.hp}/{creature.stats.max_hp}</p>
      <div className="grid grid-cols-2 gap-2 mt-2">
        <div className="flex items-center"><Sword size={16} className="mr-1" /> {creature.stats.attack}</div>
        <div className="flex items-center"><Shield size={16} className="mr-1" /> {creature.stats.defense}</div>
        <div className="flex items-center"><Zap size={16} className="mr-1" /> {creature.stats.speed}</div>
        <div className="flex items-center"><Heart size={16} className="mr-1" /> {creature.stats.sp_defense}</div>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-200 to-green-200 flex flex-col">
      {/* Battlefield Display */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent creature status */}
        <div className="row-start-1 col-start-1">
          {renderCreatureStats(opponent_creature)}
        </div>

        {/* Top-right: Opponent creature */}
        <div className="row-start-1 col-start-2 flex justify-end items-start">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/images/creatures/${opponent_creature.meta.creature_type}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>

        {/* Bottom-left: Player creature */}
        <div className="row-start-2 col-start-1 flex items-end">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image={`/images/creatures/${player_creature.meta.creature_type}_back.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>

        {/* Bottom-right: Player creature status */}
        <div className="row-start-2 col-start-2 flex justify-end items-end">
          {renderCreatureStats(player_creature)}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-800 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {player_creature.collections?.skills.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
