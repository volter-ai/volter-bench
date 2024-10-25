import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

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

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  const renderCreature = (creature: Creature, isPlayer: boolean) => (
    <Card key={creature.uid} className={`p-4 ${isPlayer ? 'order-1' : 'order-2'}`}>
      <h2 className="text-lg font-bold">{creature.display_name}</h2>
      <Progress 
        value={(creature.stats.hp / creature.stats.max_hp) * 100} 
        className="my-2"
      />
      <p className="text-sm">HP: {creature.stats.hp} / {creature.stats.max_hp}</p>
      <div className="mt-2 flex space-x-2">
        <div className="flex items-center">
          <Sword size={16} className="mr-1" />
          <span>{creature.stats.attack}</span>
        </div>
        <div className="flex items-center">
          <Shield size={16} className="mr-1" />
          <span>{creature.stats.defense}</span>
        </div>
        <div className="flex items-center">
          <Zap size={16} className="mr-1" />
          <span>{creature.stats.speed}</span>
        </div>
      </div>
    </Card>
  );

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-around p-4">
        {renderCreature(playerCreature, true)}
        {renderCreature(opponentCreature, false)}
      </div>

      {/* User Interface */}
      <Card className="m-4">
        <div className="mb-4 h-24 bg-gray-200 p-2 rounded overflow-y-auto">
          <p>What will {playerCreature.display_name} do?</p>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {playerCreature.collections.skills.map((skill) => (
            <Button
              key={skill.uid}
              variant={availableButtonSlugs.includes(skill.display_name.toLowerCase()) ? "default" : "secondary"}
              onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
              disabled={!availableButtonSlugs.includes(skill.display_name.toLowerCase())}
            >
              {skill.display_name}
            </Button>
          ))}
        </div>
      </Card>
    </div>
  );
}
