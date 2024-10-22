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
  const { availableButtonSlugs = [], emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const buttonConfig = {
    play: { text: 'Play', icon: <Play className="mr-2 h-4 w-4" /> },
    quit: { text: 'Quit', icon: <X className="mr-2 h-4 w-4" /> },
  };

  return (
    <div className="container mx-auto h-full flex flex-col justify-between p-4">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Creature Battle Game</h1>
        <p className="text-xl">Welcome, {props.data.entities.player?.display_name || 'Default Player'}!</p>
      </div>

      <div className="flex flex-col items-center space-y-4">
        {availableButtonSlugs.map((slug) => (
          <Button
            key={slug}
            onClick={() => emitButtonClick(slug)}
            className="w-48"
          >
            {buttonConfig[slug]?.icon}
            {buttonConfig[slug]?.text || slug}
          </Button>
        ))}
      </div>
    </div>
  );
}
