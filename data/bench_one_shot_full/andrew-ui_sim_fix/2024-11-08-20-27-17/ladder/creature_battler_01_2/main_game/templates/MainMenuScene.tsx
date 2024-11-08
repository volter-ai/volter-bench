import { useCurrentButtons } from "@/lib/useChoices";
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
        availableButtonSlugs = ['play', 'quit'],
        emitButtonClick = (slug: string) => console.warn(`Button ${slug} clicked but no handler available`)
    } = useCurrentButtons() ?? {};

    // Early return with basic UI if data is missing
    if (!props.data?.entities?.player) {
        return (
            <div className="w-full h-full overflow-hidden">
                <div className="w-full h-full relative bg-slate-900">
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <h1 className="text-4xl font-bold text-white mb-8">Loading Game...</h1>
                    </div>
                </div>
            </div>
        );
    }

    const handleButtonClick = (slug: string) => {
        if (availableButtonSlugs.includes(slug)) {
            try {
                emitButtonClick(slug);
            } catch (error) {
                console.error('Failed to emit button click:', error);
            }
        }
    };

    return (
        <div className="w-full h-full overflow-hidden">
            <div className="w-full h-full relative bg-slate-900">
                <div className="absolute inset-0 flex flex-col items-center justify-between py-12">
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            GAME TITLE
                        </h1>
                    </div>

                    <div className="flex flex-col gap-4 items-center mb-8">
                        {availableButtonSlugs.includes('play') && (
                            <button
                                onClick={() => handleButtonClick('play')}
                                className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
                                data-testid="play-button"
                            >
                                <Play size={24} />
                                <span>Play Game</span>
                            </button>
                        )}

                        {availableButtonSlugs.includes('quit') && (
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
