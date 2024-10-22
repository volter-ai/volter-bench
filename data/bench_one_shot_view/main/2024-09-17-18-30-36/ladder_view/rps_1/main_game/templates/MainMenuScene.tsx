import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: {
    prototype_id: string;
    category: string;
  };
  entities: Record<string, any>;
  collections: {
    skills: Skill[];
  };
  display_name: string;
  description: string;
}

interface Skill {
  uid: string;
  stats: Record<string, number>;
  meta: {
    prototype_id: string;
    category: string;
  };
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
  collections: Record<string, any>;
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
    }
  };

  return (
    <div className="@container w-full h-full flex flex-col items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600 text-white p-4">
      <Card className="@lg:w-3/4 @md:w-5/6 @sm:w-11/12 max-w-2xl bg-white/10 backdrop-blur-md rounded-xl shadow-xl p-8">
        <h1 className="text-4xl @lg:text-6xl font-bold text-center mb-8">
          {props.data.display_name || "Main Menu"}
        </h1>
        <div className="flex flex-col space-y-4">
          {currentButtonIds.includes('play') && (
            <Button
              onClick={() => handleButtonClick('play')}
              className="py-3 text-xl flex items-center justify-center"
            >
              <Play className="mr-2" /> Play Game
            </Button>
          )}
          {currentButtonIds.includes('quit') && (
            <Button
              onClick={() => handleButtonClick('quit')}
              variant="destructive"
              className="py-3 text-xl flex items-center justify-center"
            >
              <X className="mr-2" /> Quit
            </Button>
          )}
        </div>
      </Card>
      {props.data.entities.player && availableInteractiveThingIds.includes(props.data.entities.player.uid) && (
        <Alert className="mt-8 @lg:w-3/4 @md:w-5/6 @sm:w-11/12 max-w-2xl">
          <AlertTitle>Player Information</AlertTitle>
          <AlertDescription>
            {props.data.entities.player.display_name}: {props.data.entities.player.description}
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
}
