import { useCurrentButtons } from "@/lib/useChoices";
import { Play, XCircle } from 'lucide-react';
import { useEffect } from 'react';

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
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    // Use default buttons if none are available
    const buttonSlugs = availableButtonSlugs || ['play', 'quit'];

    // Register buttons with game events system
    useEffect(() => {
        if (window.gameEvents) {
            window.gameEvents.rawCurrentChoiceList = buttonSlugs;
        }
    }, [buttonSlugs]);

    const handleButtonClick = (slug: string) => {
        if (buttonSlugs.includes(slug)) {
            emitButtonClick(slug);
            // Update the remaining choices after click
            if (window.gameEvents) {
                const remainingChoices = buttonSlugs.filter(s => s !== slug);
                window.gameEvents.rawCurrentChoiceList = remainingChoices;
            }
        }
    };

    return (
        <div className="w-full h-full overflow-hidden">
            <div className="w-full h-full relative bg-slate-900">
                <div className="absolute inset-0 flex flex-col items-center justify-between py-12 aspect-video max-h-full max-w-full mx-auto">
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            GAME TITLE
                        </h1>
                    </div>

                    <div className="flex flex-col gap-4 items-center mb-8">
                        {buttonSlugs.includes('play') && (
                            <button
                                onClick={() => handleButtonClick('play')}
                                className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
                                data-testid="play-button"
                            >
                                <Play size={24} />
                                <span>Play Game</span>
                            </button>
                        )}

                        {buttonSlugs.includes('quit') && (
                            <button
                                onClick={() => handleButtonClick('quit')}
                                className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors"
                                data-testid="quit-button"
                            >
                                <XCircle size={24} />
                                <span>Quit</span>
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
