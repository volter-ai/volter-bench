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

  const handleButtonClick = (buttonId: string) => {
    if (currentButtonIds.includes(buttonId)) {
      emitButtonClick(buttonId);
    } else {
      console.warn(`Button with ID ${buttonId} is not enabled.`);
    }
  };

  return (
    <div className="flex flex-col h-full w-full p-4 bg-gray-100">
      <div className="flex-grow flex flex-col items-center justify-center">
        <h1 className="text-4xl font-bold text-center mb-8">Game Title</h1>
        <Card className="w-full max-w-md p-6 bg-white shadow-lg">
          <div className="space-y-4">
            <Button
              id="play-button"
              className="w-full"
              onClick={() => handleButtonClick('play')}
              disabled={!currentButtonIds.includes('play')}
            >
              <Play className="mr-2 h-4 w-4" /> Play Game
            </Button>
            <Button
              id="quit-button"
              className="w-full"
              variant="outline"
              onClick={() => handleButtonClick('quit')}
              disabled={!currentButtonIds.includes('quit')}
            >
              <X className="mr-2 h-4 w-4" /> Quit Game
            </Button>
          </div>
        </Card>
      </div>
      {props.data.entities.player && (
        <Alert className="mt-4">
          <AlertTitle>Welcome, {props.data.entities.player.display_name}!</AlertTitle>
          <AlertDescription>{props.data.entities.player.description}</AlertDescription>
        </Alert>
      )}
    </div>
  );
}
