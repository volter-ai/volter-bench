import React, { useState, useEffect } from 'react';
import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
  image_url: string;
}

interface Player {
  __type: "Player";
  uid: string;
  entities: {
    active_creature: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const [message, setMessage] = useState("Battle start!");

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  useEffect(() => {
    const timer = setTimeout(() => {
      setMessage("");
    }, 3000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg flex flex-col">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Opponent Status */}
          <div className="flex justify-start items-start">
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                image={opponentCreature.image_url}
                hp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
              />
            )}
          </div>

          {/* Opponent Creature */}
          <div className="flex justify-end items-start">
            {opponentCreature && (
              <img src={opponentCreature.image_url} alt={opponentCreature.display_name} className="w-48 h-48 object-contain" />
            )}
          </div>

          {/* Player Creature */}
          <div className="flex justify-start items-end">
            {playerCreature && (
              <img src={playerCreature.image_url} alt={playerCreature.display_name} className="w-48 h-48 object-contain" />
            )}
          </div>

          {/* Player Status */}
          <div className="flex justify-end items-end">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                image={playerCreature.image_url}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            )}
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-200 p-4">
          {message ? (
            <div className="text-center text-xl font-bold mb-4">{message}</div>
          ) : (
            <div className="grid grid-cols-2 gap-4">
              {availableButtonSlugs.includes('attack') && (
                <Button onClick={() => emitButtonClick('attack')}>
                  <Sword className="mr-2 h-4 w-4" /> Attack
                </Button>
              )}
              {availableButtonSlugs.includes('swap') && (
                <Button onClick={() => emitButtonClick('swap')}>
                  <Repeat className="mr-2 h-4 w-4" /> Swap
                </Button>
              )}
              {availableButtonSlugs.includes('back') && (
                <Button onClick={() => emitButtonClick('back')}>
                  <ArrowLeft className="mr-2 h-4 w-4" /> Back
                </Button>
              )}
              {playerCreature?.collections?.skills?.map((skill: Skill) => (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Base Damage: ${skill.stats.base_damage}`}
                  onClick={() => emitButtonClick('attack')}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
