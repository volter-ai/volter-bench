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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const buttonConfig = {
    play: { text: 'Play', icon: <Play className="mr-2 h-4 w-4" /> },
    quit: { text: 'Quit', icon: <X className="mr-2 h-4 w-4" /> },
  };

  return (
    <div className="container mx-auto h-full flex flex-col justify-between p-4">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Creature Battle Game</h1>
      </div>
      
      <Card className="w-full max-w-md mx-auto p-6">
        <div className="space-y-4">
          {availableButtonSlugs.map((slug) => (
            <Button
              key={slug}
              className="w-full text-lg"
              onClick={() => emitButtonClick(slug)}
            >
              {buttonConfig[slug]?.icon}
              {buttonConfig[slug]?.text || slug}
            </Button>
          ))}
        </div>
      </Card>

      {props.data.entities.player && (
        <Alert>
          <AlertTitle>Welcome, {props.data.entities.player.display_name}!</AlertTitle>
          <AlertDescription>
            Get ready for an exciting creature battle adventure.
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
}
