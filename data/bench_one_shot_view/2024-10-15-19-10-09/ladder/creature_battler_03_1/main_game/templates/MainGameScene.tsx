import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Heart, Sword, Shield, Zap } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

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
  collections: {
    skills: Skill[];
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

const CreatureCard: React.FC<{ creature: Creature; isPlayer: boolean }> = ({ creature, isPlayer }) => (
  <Card className={`p-4 ${isPlayer ? 'bg-blue-100' : 'bg-red-100'}`}>
    <h3 className="text-lg font-bold">{creature.display_name}</h3>
    <div className="flex items-center space-x-2">
      <Heart className="w-4 h-4" />
      <span>{creature.stats.hp} / {creature.stats.max_hp}</span>
    </div>
    <div className="flex space-x-2 mt-2">
      <div className="flex items-center">
        <Sword className="w-4 h-4 mr-1" />
        <span>{creature.stats.attack}</span>
      </div>
      <div className="flex items-center">
        <Shield className="w-4 h-4 mr-1" />
        <span>{creature.stats.defense}</span>
      </div>
      <div className="flex items-center">
        <Zap className="w-4 h-4 mr-1" />
        <span>{creature.stats.speed}</span>
      </div>
    </div>
  </Card>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs = [], emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="text-center">Loading game data...</div>;
  }

  const actionButtons = [
    { uid: 'lick', display_name: 'Lick' },
    { uid: 'tackle', display_name: 'Tackle' },
    ...playerCreature.collections.skills
  ];

  return (
    <div className="flex flex-col h-full w-full max-w-[177.78vh] mx-auto aspect-video bg-gray-100">
      <div className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </div>

      <div className="flex-grow flex items-center justify-between p-4">
        <CreatureCard creature={playerCreature} isPlayer={true} />
        <CreatureCard creature={opponentCreature} isPlayer={false} />
      </div>

      <div className="bg-white p-4 h-1/3">
        <Card className="h-full flex flex-col">
          <div className="flex-grow p-2 overflow-y-auto">
            <p>Battle in progress...</p>
          </div>
          <div className="flex justify-center space-x-2 p-2">
            {actionButtons.map((action) => (
              <Button
                key={action.uid}
                uid={action.uid}
                onClick={() => emitButtonClick(action.uid)}
                disabled={!availableButtonSlugs.includes(action.uid)}
              >
                {action.display_name}
              </Button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
