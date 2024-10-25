import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface GameUIData {
  entities: {
    player: {
      uid: string;
      stats: Record<string, number>;
      meta: Record<string, any>;
      entities: Record<string, any>;
      collections: Record<string, any>;
      display_name: string;
      description: string;
    };
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const buttonConfig = [
    { id: 'play', label: 'Play', icon: Play },
    { id: 'quit', label: 'Quit', icon: X },
  ];

  return (
    <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 p-8">
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-white text-center">
          {props.data.entities.player?.display_name || "Game Title"}
        </h1>
      </div>
      
      <div className="flex flex-col items-center space-y-4">
        {buttonConfig.map((button) => (
          availableButtonSlugs.includes(button.id) && (
            <Button
              key={button.id}
              onClick={() => emitButtonClick(button.id)}
              className="w-48 h-12 text-lg"
            >
              <button.icon className="mr-2 h-5 w-5" />
              {button.label}
            </Button>
          )
        ))}
      </div>
    </div>
  );
}
