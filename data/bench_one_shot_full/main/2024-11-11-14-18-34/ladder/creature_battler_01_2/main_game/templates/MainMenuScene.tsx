import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
}

export function MainMenuSceneView(props: { data?: GameUIData }) {
    const {
        availableButtonSlugs = ['play', 'quit'], // Default buttons always available
        emitButtonClick = (slug: string) => console.warn(`Button click not handled: ${slug}`)
    } = useCurrentButtons();

    const handleButtonClick = (slug: string) => {
        if (availableButtonSlugs.includes(slug)) {
            emitButtonClick(slug);
        }
    };

    return (
        <div className="w-full h-full overflow-hidden" data-testid="main-menu-scene">
            <div className="w-full h-full relative bg-slate-900">
                <div className="absolute inset-0 flex flex-col items-center justify-between py-12">
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            GAME TITLE
                        </h1>
                    </div>

                    <div className="flex flex-col gap-4 items-center mb-8" data-testid="menu-buttons">
                        <button
                            onClick={() => handleButtonClick('play')}
                            className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
                            role="button"
                            data-testid="play-button"
                            aria-label="Play Game"
                        >
                            <Play size={24} />
                            <span>Play Game</span>
                        </button>

                        <button
                            onClick={() => handleButtonClick('quit')}
                            className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors"
                            role="button"
                            data-testid="quit-button"
                            aria-label="Quit Game"
                        >
                            <XCircle size={24} />
                            <span>Quit</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
