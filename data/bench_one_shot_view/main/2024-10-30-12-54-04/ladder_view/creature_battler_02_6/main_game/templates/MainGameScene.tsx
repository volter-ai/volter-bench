import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
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

const CreatureDisplay = ({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) => (
  <Card className={`p-4 ${isPlayer ? 'order-1' : 'order-2'}`}>
    <h2 className="text-lg font-bold">{creature?.display_name || 'Unknown Creature'}</h2>
    <Progress value={(creature?.stats.hp / creature?.stats.max_hp) * 100 || 0} className="my-2" />
    <div className="text-sm">HP: {creature?.stats.hp || 0} / {creature?.stats.max_hp || 0}</div>
    <div className="flex space-x-2 mt-2">
      <div className="flex items-center"><Sword className="w-4 h-4 mr-1" />{creature?.stats.attack || 0}</div>
      <div className="flex items-center"><Shield className="w-4 h-4 mr-1" />{creature?.stats.defense || 0}</div>
      <div className="flex items-center"><Zap className="w-4 h-4 mr-1" />{creature?.stats.speed || 0}</div>
    </div>
  </Card>
);

export function MainGameSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = data?.entities?.player_creature;
  const opponentCreature = data?.entities?.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      <Card className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </Card>

      <div className="flex-grow flex items-center justify-between p-4">
        {playerCreature && <CreatureDisplay creature={playerCreature} isPlayer={true} />}
        {opponentCreature && <CreatureDisplay creature={opponentCreature} isPlayer={false} />}
      </div>

      <Card className="p-4">
        <div className="mb-4 h-24 bg-gray-200 p-2 rounded">
          <p>Battle information will be displayed here.</p>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {playerCreature?.collections.skills.map((skill) => (
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
