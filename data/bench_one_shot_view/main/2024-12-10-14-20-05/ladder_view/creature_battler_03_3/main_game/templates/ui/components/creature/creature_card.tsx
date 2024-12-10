import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let BaseCard = withClickable(({ uid, ...props }: BaseCardProps) => (
  <Card {...props} />
))

let BaseCardHeader = withClickable(({ uid, ...props }: BaseCardProps) => (
  <CardHeader {...props} />
))

let BaseCardContent = withClickable(({ uid, ...props }: BaseCardProps) => (
  <CardContent {...props} />
))

let BaseCardFooter = withClickable(({ uid, ...props }: BaseCardProps) => (
  <CardFooter {...props} />
))

let BaseCardTitle = withClickable(({ uid, ...props }: BaseCardProps & React.HTMLAttributes<HTMLHeadingElement>) => (
  <CardTitle {...props} />
))

let BaseCardDescription = withClickable(({ uid, ...props }: BaseCardProps & React.HTMLAttributes<HTMLParagraphElement>) => (
  <CardDescription {...props} />
))

interface CreatureCardProps extends BaseCardProps {
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => (
    <BaseCard ref={ref} uid={`${uid}-card`} className={cn("w-[350px]", className)} {...props}>
      <BaseCardHeader uid={`${uid}-header`}>
        <BaseCardTitle uid={`${uid}-title`}>{name}</BaseCardTitle>
        <BaseCardDescription uid={`${uid}-description`}>HP: {hp}/{maxHp}</BaseCardDescription>
      </BaseCardHeader>
      <BaseCardContent uid={`${uid}-content`}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-contain"
        />
      </BaseCardContent>
      <BaseCardFooter uid={`${uid}-footer`} className="flex justify-between" />
    </BaseCard>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
