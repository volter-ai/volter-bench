import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { currentButtonIds, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const isButtonAvailable = (id: string) => currentButtonIds.includes(id);

  return (
    <div className="flex flex-col h-full w-full p-4 bg-gray-100">
      <div className="flex-grow flex flex-col items-center justify-between">
        <h1 className="text-4xl font-bold text-center text-blue-600 mb-8">
          {props.data.display_name || "Game Title"}
        </h1>

        <div className="mt-auto space-y-4">
          <Button
            className="w-full"
            onClick={() => emitButtonClick('play')}
            disabled={!isButtonAvailable('play')}
          >
            <Play className="mr-2 h-4 w-4" /> Play Game
          </Button>
          <Button
            className="w-full"
            variant="outline"
            onClick={() => emitButtonClick('quit')}
            disabled={!isButtonAvailable('quit')}
          >
            <X className="mr-2 h-4 w-4" /> Quit Game
          </Button>
        </div>
      </div>

      {props.data.entities.player && (
        <Card className="mt-4 p-4">
          <h2 className="text-xl font-semibold mb-2">Player Info</h2>
          <p>Name: {props.data.entities.player.display_name}</p>
          <p>Description: {props.data.entities.player.description}</p>
        </Card>
      )}
    </div>
  );
}
