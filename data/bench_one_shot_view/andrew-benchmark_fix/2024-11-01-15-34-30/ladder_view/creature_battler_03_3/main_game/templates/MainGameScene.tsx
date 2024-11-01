import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

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
  <Card className={`flex flex-col items-center p-4 ${isPlayer ? 'order-1' : 'order-2'}`}>
    <div className="text-lg font-bold">{creature.display_name}</div>
    <div className="w-32 h-32 bg-gray-300 rounded-full flex items-center justify-center mb-2">
      {creature.meta.creature_type}
    </div>
    <Progress 
      value={(creature.stats.hp / creature.stats.max_hp) * 100} 
      className="w-full h-2.5 mb-1"
    />
    <div className="text-sm">{creature.stats.hp} / {creature.stats.max_hp} HP</div>
    <div className="flex space-x-2 mt-2">
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
    <div className="flex flex-col h-screen w-full max-w-[177.78vh] mx-auto" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <Card className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </Card>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-around bg-green-100 p-4">
        {player_creature && <CreatureDisplay creature={player_creature} isPlayer={true} />}
        {opponent_creature && <CreatureDisplay creature={opponent_creature} isPlayer={false} />}
      </div>

      {/* User Interface */}
      <Card className="bg-gray-100 p-4 h-1/3">
        <div className="bg-white rounded-lg p-4 h-full flex flex-col">
          <div className="flex-grow mb-4 overflow-y-auto">
            <p>Battle information and descriptions will appear here.</p>
          </div>
          <div className="flex flex-wrap justify-center gap-2">
            {availableButtonSlugs.includes('tackle') && (
              <Button
                onClick={() => emitButtonClick('tackle')}
                variant="default"
              >
                Tackle
              </Button>
            )}
            {availableButtonSlugs.includes('lick') && (
              <Button
                onClick={() => emitButtonClick('lick')}
                variant="default"
              >
                Lick
              </Button>
            )}
          </div>
        </div>
      </Card>
    </div>
  );
}
