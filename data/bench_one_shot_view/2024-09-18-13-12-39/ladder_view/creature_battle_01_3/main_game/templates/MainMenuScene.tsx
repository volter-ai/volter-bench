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
  collections: Record<string, any>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const handleButtonClick = (slug: string) => {
    if (availableButtonSlugs && availableButtonSlugs.includes(slug)) {
      emitButtonClick(slug);
    }
  };

  const player = props.data.entities?.player;

  return (
    <div className="cq-h-full cq-w-full flex flex-col justify-between items-center p-4 bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="cq-w-full cq-h-1/3 flex justify-center items-center">
        <Card className="cq-w-2/3 cq-h-full flex items-center justify-center bg-opacity-80 backdrop-blur-md">
          <h1 className="text-4xl font-bold text-white">Game Title</h1>
        </Card>
      </div>

      <div className="cq-w-full cq-h-1/3 flex justify-center items-center">
        {/* Middle section for potential future content */}
      </div>

      <div className="cq-w-full cq-h-1/3 flex justify-center items-end">
        <Card className="cq-w-2/3 p-4 bg-opacity-80 backdrop-blur-md">
          <div className="flex justify-center space-x-4">
            <Button
              onClick={() => handleButtonClick('play')}
              disabled={!availableButtonSlugs || !availableButtonSlugs.includes('play')}
              className="cq-w-1/3 cq-h-16 text-xl"
            >
              <Play className="mr-2" /> Play
            </Button>
            <Button
              onClick={() => handleButtonClick('quit')}
              disabled={!availableButtonSlugs || !availableButtonSlugs.includes('quit')}
              className="cq-w-1/3 cq-h-16 text-xl"
              variant="destructive"
            >
              <X className="mr-2" /> Quit
            </Button>
          </div>
        </Card>
      </div>

      {player && (
        <Alert className="mt-4 cq-w-2/3">
          <AlertTitle>Welcome, {player.display_name}!</AlertTitle>
          <AlertDescription>{player.description}</AlertDescription>
        </Alert>
      )}
    </div>
  );
}
