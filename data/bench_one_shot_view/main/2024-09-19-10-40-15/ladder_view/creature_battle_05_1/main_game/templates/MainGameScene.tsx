import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Heart, Swords, ArrowLeft, SwapHorizontal } from 'lucide-react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
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

export function MainGameSceneView(props: { data: GameUIData }) {
  const { currentButtonIds, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const player = props.data.entities.player;
  const opponent = props.data.entities.bot;

  const renderCreature = (creature: Creature, isPlayer: boolean) => (
    <div className={`flex flex-col items-center ${isPlayer ? 'justify-end' : 'justify-start'}`}>
      <div className="w-32 h-32 bg-gray-200 rounded-full mb-2"></div>
      <Card className="p-2">
        <h3 className="text-lg font-bold">{creature.display_name}</h3>
        <div className="flex items-center">
          <Heart className="w-4 h-4 mr-1" />
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-green-600 h-2.5 rounded-full"
              style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
            ></div>
          </div>
          <span className="ml-2 text-sm">
            {creature.stats.hp}/{creature.stats.max_hp}
          </span>
        </div>
      </Card>
    </div>
  );

  return (
    <div className="cq-container w-full h-full flex flex-col">
      <div className="flex-grow flex flex-col">
        <div className="flex-grow flex justify-between items-stretch p-4">
          {renderCreature(opponent.entities.active_creature, false)}
          {renderCreature(player.entities.active_creature, true)}
        </div>
      </div>
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {currentButtonIds.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')}>
              <Swords className="w-4 h-4 mr-2" /> Attack
            </Button>
          )}
          {currentButtonIds.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <SwapHorizontal className="w-4 h-4 mr-2" /> Swap
            </Button>
          )}
          {currentButtonIds.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="w-4 h-4 mr-2" /> Back
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
