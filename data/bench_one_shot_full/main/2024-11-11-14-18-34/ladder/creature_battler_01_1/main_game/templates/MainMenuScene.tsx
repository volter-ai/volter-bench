import { useCurrentButtons } from "@/lib/useChoices";
import { Play, XCircle } from 'lucide-react';

interface ExamplePlayer {
    uid: string;
    stats: {
        stat1: number;
    };
}

interface GameUIData {
    entities: {
        player: ExamplePlayer;
    };
}

const DEFAULT_BUTTON_SLUGS = ['play', 'quit'];

export function MainMenuSceneView(props: { data?: GameUIData }) {
    const {
        availableButtonSlugs = DEFAULT_BUTTON_SLUGS,
        emitButtonClick = () => console.warn('Button handler not initialized')
    } = useCurrentButtons() || {};

    // Show a basic error UI if data is explicitly null or undefined
    if (props.data === null || props.data === undefined) {
        return (
            <div className="w-full h-full flex items-center justify-center bg-slate-900">
                <h1 className="text-2xl text-white">Loading game data...</h1>
            </div>
        );
    }

    const buttonSlugs = Array.isArray(availableButtonSlugs) ? availableButtonSlugs : DEFAULT_BUTTON_SLUGS;

    const handleButtonClick = (slug: string) => {
        try {
            emitButtonClick(slug);
        } catch (error) {
            console.error('Failed to handle button click:', error);
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
                        {buttonSlugs.includes('play') && (
                            <button
                                onClick={() => handleButtonClick('play')}
                                className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
                            >
                                <Play size={24} />
                                <span>Play Game</span>
                            </button>
                        )}

                        {buttonSlugs.includes('quit') && (
                            <button
                                onClick={() => handleButtonClick('quit')}
                                className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors"
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
