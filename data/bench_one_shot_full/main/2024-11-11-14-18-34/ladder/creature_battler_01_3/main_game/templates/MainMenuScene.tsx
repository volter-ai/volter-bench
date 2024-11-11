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

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs = ['play', 'quit'], // Default values
        emitButtonClick
    } = useCurrentButtons();

    return (
        <div className="w-full h-full bg-slate-900 flex flex-col items-center justify-between p-12">
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    GAME TITLE
                </h1>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-4 items-center">
                {Array.isArray(availableButtonSlugs) && availableButtonSlugs.map(slug => {
                    if (slug === 'play') {
                        return (
                            <button
                                key="play-button"
                                onClick={() => emitButtonClick('play')}
                                className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
                            >
                                <Play size={24} />
                                <span>Play Game</span>
                            </button>
                        );
                    }
                    if (slug === 'quit') {
                        return (
                            <button
                                key="quit-button"
                                onClick={() => emitButtonClick('quit')}
                                className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors"
                            >
                                <XCircle size={24} />
                                <span>Quit</span>
                            </button>
                        );
                    }
                    return null;
                })}
            </div>
        </div>
    );
}
