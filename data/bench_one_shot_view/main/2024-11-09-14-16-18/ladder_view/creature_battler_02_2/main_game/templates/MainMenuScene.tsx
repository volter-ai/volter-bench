import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface GameUIData {
  entities: {
    player: {
      uid: string;
      display_name: string;
      description: string;
    }
  }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  return (
    <div 
      className="w-full h-full aspect-video relative flex flex-col items-center justify-between p-8"
      style={{
        backgroundImage: 'linear-gradient(to bottom, rgba(0,0,0,0.7), rgba(0,0,0,0.9)), url("/menu-bg.jpg")',
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }}
    >
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-white tracking-wider">
          {props.data?.entities?.player?.display_name || "Creature Game"}
        </h1>
      </div>

      <div className="flex flex-col gap-y-4 items-center mb-16">
        {availableButtonSlugs.includes('play') && (
          <Button
            variant="default"
            size="lg"
            onClick={() => emitButtonClick('play')}
            className="w-48 flex items-center gap-x-2"
          >
            <Play className="w-5 h-5" />
            Play Game
          </Button>
        )}

        {availableButtonSlugs.includes('quit') && (
          <Button
            variant="destructive"
            size="lg"
            onClick={() => emitButtonClick('quit')}
            className="w-48 flex items-center gap-x-2"
          >
            <XCircle className="w-5 h-5" />
            Quit
          </Button>
        )}
      </div>
    </div>
  );
}
