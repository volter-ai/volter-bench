import { useCurrentButtons } from "@/lib/useChoices";
import { Play, XCircle } from 'lucide-react';
import { useEffect, useState } from 'react';

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
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    const {
        availableButtonSlugs = ['play', 'quit'],  // Set default buttons
        emitButtonClick
    } = useCurrentButtons() || {}; // Add fallback for hook

    useEffect(() => {
        let mounted = true;

        const initializeMenu = async () => {
            try {
                // Check for both data and required nested properties
                if (props.data?.entities?.player) {
                    if (mounted) {
                        setIsLoading(false);
                    }
                } else {
                    throw new Error('Invalid game data structure');
                }
            } catch (err) {
                if (mounted) {
                    setError('Failed to initialize menu');
                    console.error('Menu initialization error:', err);
                }
            }
        };

        initializeMenu();

        return () => {
            mounted = false;
        };
    }, [props.data]);

    if (error) {
        return (
            <div className="w-full h-full flex items-center justify-center bg-slate-900" data-testid="error-container">
                <p className="text-red-500">{error}</p>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="w-full h-full flex items-center justify-center bg-slate-900" data-testid="loading-container">
                <p className="text-white">Loading...</p>
            </div>
        );
    }

    const handleButtonClick = (slug: string) => {
        if (emitButtonClick && availableButtonSlugs.includes(slug)) {
            emitButtonClick(slug);
        }
    };

    return (
        <div className="w-full h-full overflow-hidden" data-testid="main-menu-container">
            <div className="w-full h-full relative bg-slate-900">
                <div className="absolute inset-0 flex flex-col items-center justify-between py-12 aspect-video max-h-full max-w-full mx-auto">
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
