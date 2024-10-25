import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: {
    creature_type: string;
  };
}

interface Player {
  uid: string;
  entities: {
    active_creature: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    bot: Player;
  };
}

const CreatureDisplay: React.FC<{ creature: Creature; isPlayer: boolean }> = ({ creature, isPlayer }) => (
  <div className={`flex flex-col items-center ${isPlayer ? 'justify-end' : 'justify-start'}`}>
    <div className="w-32 h-32 bg-gray-300 rounded-full mb-2"></div>
    <div className="text-center">
      <p className="font-bold">{creature.display_name}</p>
      <p>Type: {creature.meta.creature_type}</p>
    </div>
  </div>
);

const CreatureStatus: React.FC<{ creature: Creature }> = ({ creature }) => (
  <Card className="p-4">
    <h3 className="font-bold">{creature.display_name}</h3>
    <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
      <div 
        className="bg-blue-600 h-2.5 rounded-full" 
        style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
      ></div>
    </div>
    <p>{creature.stats.hp} / {creature.stats.max_hp} HP</p>
  </Card>
);

const ActionButtons: React.FC<{ 
  availableButtons: string[]; 
  onButtonClick: (slug: string) => void;
  availableCreatures: string[];
  onCreatureClick: (uid: string) => void;
}> = ({ availableButtons, onButtonClick, availableCreatures, onCreatureClick }) => (
  <div className="grid grid-cols-2 gap-4">
    {availableButtons.includes('attack') && (
      <Button onClick={() => onButtonClick('attack')}>
        <Sword className="mr-2 h-4 w-4" /> Attack
      </Button>
    )}
    {availableButtons.includes('swap') && (
      <Button onClick={() => onButtonClick('swap')}>
        <Repeat className="mr-2 h-4 w-4" /> Swap
      </Button>
    )}
    {availableButtons.includes('back') && (
      <Button onClick={() => onButtonClick('back')}>
        <ArrowLeft className="mr-2 h-4 w-4" /> Back
      </Button>
    )}
    {availableCreatures.map((creatureUid) => (
      <Button key={creatureUid} onClick={() => onCreatureClick(creatureUid)}>
        Select Creature
      </Button>
    ))}
  </div>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const playerCreature = props.data.entities.player.entities.active_creature;
  const botCreature = props.data.entities.bot.entities.active_creature;

  return (
    <div className="@container w-full h-full flex flex-col">
      <div className="flex-grow flex flex-col @[900px]:flex-row">
        <div className="flex-1 p-4 flex flex-col justify-between">
          <CreatureStatus creature={botCreature} />
          <CreatureDisplay creature={botCreature} isPlayer={false} />
        </div>
        <div className="flex-1 p-4 flex flex-col justify-between">
          <CreatureDisplay creature={playerCreature} isPlayer={true} />
          <CreatureStatus creature={playerCreature} />
        </div>
      </div>
      <div className="h-1/3 p-4 bg-gray-100">
        <ActionButtons 
          availableButtons={availableButtonSlugs} 
          onButtonClick={emitButtonClick}
          availableCreatures={availableInteractiveThingIds}
          onCreatureClick={emitThingClick}
        />
      </div>
    </div>
  );
}
