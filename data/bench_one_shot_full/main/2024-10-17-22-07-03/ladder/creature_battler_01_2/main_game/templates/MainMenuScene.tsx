import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button";

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
  stats: Record<string, number>;
  meta: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const renderButtons = () => {
    const buttonConfig = [
      { id: 'play', label: 'Play', icon: <Play className="mr-2 h-4 w-4" /> },
      { id: 'quit', label: 'Quit', icon: <X className="mr-2 h-4 w-4" /> },
    ];

    return buttonConfig.map(button => {
      if (availableButtonSlugs.includes(button.id)) {
        return (
          <Button
            key={button.id}
            onClick={() => emitButtonClick(button.id)}
            className="w-48"
          >
            {button.icon}
            {button.label}
          </Button>
        );
      }
      return null;
    });
  };

  return (
    <div className="w-full h-full aspect-video bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8" data-uid={data.uid}>
      <h1 className="text-4xl font-bold text-white mt-16">
        {data.display_name || "Game Title"}
      </h1>
      <div className="flex flex-col space-y-4 mb-16">
        {renderButtons()}
      </div>
    </div>
  );
}
