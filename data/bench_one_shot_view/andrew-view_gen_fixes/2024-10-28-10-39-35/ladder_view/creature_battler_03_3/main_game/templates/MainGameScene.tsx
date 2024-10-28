import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Sword, Shield, Zap } from 'lucide-react';

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
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
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

const CreatureDisplay = ({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) => (
  <Card className={`p-4 ${isPlayer ? 'order-1' : 'order-2'}`}>
    <h2 className="text-lg font-bold">{creature.display_name}</h2>
    <div className="w-32 h-32 bg-gray-300 rounded-full mb-2 mx-auto"></div>
    <Progress value={(creature.stats.hp / creature.stats.max_hp) * 100} className="w-full h-2" />
    <p className="text-sm text-center">{`HP: ${creature.stats.hp}/${creature.stats.max_hp}`}</p>
    <div className="flex justify-center space-x-2 mt-2">
      <span title="Attack"><Sword size={16} /> {creature.stats.attack}</span>
      <span title="Defense"><Shield size={16} /> {creature.stats.defense}</span>
      <span title="Speed"><Zap size={16} /> {creature.stats.speed}</span>
    </div>
  </Card>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="flex flex-col h-full w-full max-w-[177.78vh] max-h-[56.25vw] mx-auto bg-gray-100">
      {/* HUD */}
      <Card className="bg-blue-500 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </Card>

      {/* Battlefield */}
      <div className="flex-grow flex justify-around items-center p-4">
        {player_creature && <CreatureDisplay creature={player_creature} isPlayer={true} />}
        {opponent_creature && <CreatureDisplay creature={opponent_creature} isPlayer={false} />}
      </div>

      {/* User Interface */}
      <Card className="p-4 h-1/3">
        <Card className="bg-gray-200 p-2 mb-2 h-20 overflow-y-auto">
          <p>Battle information and descriptions will appear here.</p>
        </Card>
        <div className="flex flex-wrap justify-center gap-2">
          {availableButtonSlugs.includes('tackle') && (
            <Button onClick={() => emitButtonClick('tackle')}>
              Tackle
            </Button>
          )}
          {availableButtonSlugs.includes('lick') && (
            <Button onClick={() => emitButtonClick('lick')}>
              Lick
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
