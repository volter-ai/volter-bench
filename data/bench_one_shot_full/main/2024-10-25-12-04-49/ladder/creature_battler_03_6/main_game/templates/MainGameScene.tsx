import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Sword, Shield, Zap } from 'lucide-react';

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

const ButtonArea = ({ availableButtonSlugs, emitButtonClick }: { availableButtonSlugs: string[], emitButtonClick: (slug: string) => void }) => {
  const buttonConfig = [
    { slug: 'play-again', label: 'Play Again' },
    { slug: 'quit-game', label: 'Quit Game' },
  ];

  return (
    <div className="flex space-x-2">
      {buttonConfig.map(({ slug, label }) => (
        availableButtonSlugs.includes(slug) && (
          <Button key={slug} onClick={() => emitButtonClick(slug)}>{label}</Button>
        )
      ))}
    </div>
  );
};

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        {player_creature && (
          <div className="flex flex-col items-center">
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              imageUrl="/placeholder-creature.png"
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
            />
            <div className="mt-2 flex space-x-2">
              <span><Sword size={16} /> {player_creature.stats.attack}</span>
              <span><Shield size={16} /> {player_creature.stats.defense}</span>
              <span><Zap size={16} /> {player_creature.stats.speed}</span>
            </div>
          </div>
        )}
        {opponent_creature && (
          <div className="flex flex-col items-center">
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              imageUrl="/placeholder-creature.png"
              hp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
            />
            <div className="mt-2 flex space-x-2">
              <span><Sword size={16} /> {opponent_creature.stats.attack}</span>
              <span><Shield size={16} /> {opponent_creature.stats.defense}</span>
              <span><Zap size={16} /> {opponent_creature.stats.speed}</span>
            </div>
          </div>
        )}
      </div>

      {/* User Interface */}
      <Card className="p-4 m-4">
        <h2 className="text-lg font-semibold mb-2">Actions</h2>
        <div className="grid grid-cols-2 gap-2">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
            />
          ))}
        </div>
        <div className="mt-4">
          <ButtonArea availableButtonSlugs={availableButtonSlugs} emitButtonClick={emitButtonClick} />
        </div>
      </Card>
    </div>
  );
}
