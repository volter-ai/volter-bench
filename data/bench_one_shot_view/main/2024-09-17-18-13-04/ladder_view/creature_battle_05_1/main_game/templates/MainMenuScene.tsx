import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { currentButtonIds, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const handleButtonClick = (buttonId: string) => {
    if (currentButtonIds.includes(buttonId)) {
      emitButtonClick(buttonId);
    }
  };

  return (
    <div className="container mx-auto h-full flex flex-col justify-between p-4">
      <div className="flex-1 flex items-center justify-center">
        <Card className="w-full max-w-2xl aspect-video bg-gradient-to-b from-blue-500 to-blue-700 flex items-center justify-center">
          <h1 className="text-4xl md:text-6xl font-bold text-white">Game Title</h1>
        </Card>
      </div>
      <div className="flex justify-center space-x-4 mt-8">
        <Button
          onClick={() => handleButtonClick('play')}
          disabled={!currentButtonIds.includes('play')}
          className="px-8 py-4 text-lg"
        >
          <Play className="mr-2 h-6 w-6" /> Play
        </Button>
        <Button
          onClick={() => handleButtonClick('quit')}
          disabled={!currentButtonIds.includes('quit')}
          className="px-8 py-4 text-lg"
          variant="destructive"
        >
          <X className="mr-2 h-6 w-6" /> Quit
        </Button>
      </div>
      {props.data.entities.player && (
        <Alert className="mt-4">
          <AlertTitle>Welcome, {props.data.entities.player.display_name}!</AlertTitle>
          <AlertDescription>
            Get ready for an exciting adventure!
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
}
