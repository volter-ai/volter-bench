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

  const handleButtonClick = (slug: string) => {
    if (availableButtonSlugs.includes(slug)) {
      emitButtonClick(slug);
    }
  };

  return (
    <div className="cq-h-full cq-w-full flex flex-col justify-between items-center p-8 bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-white mb-4">Creature Battle</h1>
        <p className="text-xl text-white">
          Welcome, {props.data.entities.player?.display_name || 'Player'}!
        </p>
      </div>

      <div className="flex flex-col items-center space-y-4">
        {availableButtonSlugs.includes('play') && (
          <Button
            onClick={() => handleButtonClick('play')}
            className="w-48 h-16 text-xl"
          >
            <Play className="mr-2 h-6 w-6" /> Play
          </Button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <Button
            onClick={() => handleButtonClick('quit')}
            variant="outline"
            className="w-48 h-16 text-xl"
          >
            <X className="mr-2 h-6 w-6" /> Quit
          </Button>
        )}
      </div>
    </div>
  );
}
