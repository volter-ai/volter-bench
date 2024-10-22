import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { PlayCircle, XCircle } from 'lucide-react';

interface Player {
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  display_name: string;
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
    <div className="@container w-full h-full flex flex-col items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600 text-white p-4">
      <Card className="@lg:w-3/4 @md:w-5/6 @sm:w-11/12 max-w-2xl bg-white/10 backdrop-blur-md rounded-xl shadow-xl p-8">
        <h1 className="text-4xl @lg:text-6xl font-bold text-center mb-8">
          {props.data.display_name || "Main Menu"}
        </h1>
        
        <div className="space-y-4">
          {currentButtonIds.includes('play') && (
            <Button
              className="w-full py-3 text-xl font-semibold"
              onClick={() => handleButtonClick('play')}
            >
              <PlayCircle className="mr-2 h-6 w-6" />
              Play
            </Button>
          )}
          
          {currentButtonIds.includes('quit') && (
            <Button
              className="w-full py-3 text-xl font-semibold"
              onClick={() => handleButtonClick('quit')}
              variant="secondary"
            >
              <XCircle className="mr-2 h-6 w-6" />
              Quit
            </Button>
          )}
        </div>

        {props.data.entities.player && (
          <Alert className="mt-8">
            <AlertTitle>Welcome, {props.data.entities.player.display_name}!</AlertTitle>
            <AlertDescription>{props.data.entities.player.description}</AlertDescription>
          </Alert>
        )}
      </Card>
    </div>
  );
}
