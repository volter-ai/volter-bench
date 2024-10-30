import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Container } from "@/components/ui/container";

interface GameUIData {
  entities: {
    player: {
      uid: string;
      display_name: string;
    };
  };
  uid: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerName = props.data.entities.player?.display_name || "Player";

  return (
    <Container uid={props.data.uid} className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] aspect-video bg-black bg-opacity-50 text-white p-8 flex flex-col justify-between">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">Creature Battle Game</h1>
          <p className="text-xl">Welcome, {playerName}!</p>
        </div>
        
        <div className="flex flex-col items-center">
          {availableButtonSlugs.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center w-48 bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded mb-4"
            >
              <Play className="mr-2" />
              Play Game
            </button>
          )}
          
          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center w-48 bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
            >
              <X className="mr-2" />
              Quit Game
            </button>
          )}
        </div>
      </div>
    </Container>
  );
}
