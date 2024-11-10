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
        availableButtonSlugs = ['play', 'quit'],
        emitButtonClick
    } = useCurrentButtons() || {};

    useEffect(() => {
        let mounted = true;

        const initializeComponent = async () => {
            try {
                if (!emitButtonClick) {
                    throw new Error('Button handlers not initialized');
                }
                
                if (mounted) {
                    setIsLoading(false);
                }
            } catch (err) {
                if (mounted) {
                    setError(err instanceof Error ? err.message : 'Failed to initialize menu');
                    console.error(err);
                }
            }
        };

        initializeComponent();

        return () => {
            mounted = false;
        };
    }, [emitButtonClick]);

    const handleButtonClick = (slug: string) => {
        if (!emitButtonClick || !availableButtonSlugs?.includes(slug)) {
            console.error(`Invalid button click: ${slug}`);
            return;
        }
        emitButtonClick(slug);
    };

    if (error) {
        return (
            <div className="w-full h-full flex items-center justify-center bg-slate-900">
                <p className="text-red-500">Error: {error}</p>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="w-full h-full flex items-center justify-center bg-slate-900">
                <p className="text-white">Loading...</p>
            </div>
        );
    }

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
                        {availableButtonSlugs?.includes('play') && (
                            <button
                                onClick={() => handleButtonClick('play')}
                                className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
                                aria-label="Play Game"
                                role="button"
                                tabIndex={0}
                            >
                                <Play size={24} />
                                <span>Play Game</span>
                            </button>
                        )}

                        {availableButtonSlugs?.includes('quit') && (
                            <button
                                onClick={() => handleButtonClick('quit')}
                                className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors"
                                aria-label="Quit Game"
                                role="button"
                                tabIndex={0}
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
