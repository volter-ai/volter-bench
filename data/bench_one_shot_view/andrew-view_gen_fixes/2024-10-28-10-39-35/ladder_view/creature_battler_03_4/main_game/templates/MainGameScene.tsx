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
  skills: Skill[];
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
    <h3 className="text-lg font-bold">{creature.display_name}</h3>
    <div className="w-24 h-24 bg-gray-300 rounded-full mb-2"></div>
    <Progress 
      value={(creature.stats.hp / creature.stats.max_hp) * 100} 
      className="w-full h-2.5"
    />
    <p className="text-sm">{`HP: ${creature.stats.hp}/${creature.stats.max_hp}`}</p>
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

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="flex flex-col h-screen w-full max-w-[177.78vh] mx-auto" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <Card className="bg-gray-800 text-white p-2 flex justify-between items-center rounded-none">
        <div>{props.data.entities.player.display_name}</div>
        <div>{props.data.entities.opponent.display_name}</div>
      </Card>

      {/* Battlefield */}
      <div className="flex-grow flex justify-around items-center bg-green-100 p-4">
        <CreatureDisplay creature={playerCreature} isPlayer={true} />
        <CreatureDisplay creature={opponentCreature} isPlayer={false} />
      </div>

      {/* User Interface */}
      <Card className="p-4 flex-shrink-0" style={{ height: '30%' }}>
        <div className="mb-4">
          <p>Welcome to Creature Battle!</p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          {playerCreature?.skills?.map((skill) => (
            <Button
              key={skill.uid}
              onClick={() => availableButtonSlugs.includes(skill.uid) && emitButtonClick(skill.uid)}
              variant="default"
              className="w-full"
              disabled={!availableButtonSlugs.includes(skill.uid)}
            >
              {skill.display_name}
            </Button>
          ))}
        </div>
      </Card>
    </div>
  );
}
