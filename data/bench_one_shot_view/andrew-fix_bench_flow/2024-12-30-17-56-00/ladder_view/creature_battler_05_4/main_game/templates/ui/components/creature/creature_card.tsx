import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import withClickable from "@/lib/withClickable.tsx"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string;
  name: string;
  image: string;
  hp: number;
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ uid, name, image, hp, className, ...props }, ref) => (
    <Card ref={ref} className={className} {...props}>
      <CardHeader>
        <CardTitle>{name}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={image} alt={`${name} image`} className="w-full h-auto" />
      </CardContent>
      <CardFooter>
        <div className="w-full bg-gray-200 rounded-full">
          <div
            className="bg-green-500 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full"
            style={{ width: `${hp}%` }}
          >
            {hp} HP
          </div>
        </div>
      </CardFooter>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
